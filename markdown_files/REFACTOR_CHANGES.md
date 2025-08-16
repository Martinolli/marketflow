# Changes Proposal

## Introduction

Of course! This is an excellent architectural improvement. Your intuition is spot on: instead of creating fragmented, single-ticker vector stores, you should create a unified vector store for each batch analysis. This allows the RAG system to access and compare information across all recently analyzed tickers.

The core idea is to shift the responsibility of creating and saving the `TransientVectorMemory` (TVM) from the single-analysis script (`marketflow_analysis.py`) to a new batch orchestrator script. This new script will:

    1.  Initialize **one** TVM instance for the entire batch.
    2.  Define a **single, shared namespace** for the batch (e.g., `batch_analysis:20231027_153000`).
    3.  Loop through each ticker, calling `run_analysis` to generate the report and narrative.
    4.  **Upsert** the narrative for each ticker into the shared TVM, making sure to include the ticker symbol in the metadata.
    5.  After all tickers are processed, save the **single, consolidated TVM store** for the Q&A app to load.

Here is the step-by-step implementation plan:

### Step 1: Create a New Batch Orchestrator Script

We'll create a new file, `marketflow_batch_analysis.py`, which will be the main entry point for running analysis on multiple tickers.

**File: `marketflow_batch_analysis.py` (New File)**

    ```python

    """
    Marketflow Batch Analysis Orchestrator
    This script runs market analysis for multiple tickers, generates reports,
    and consolidates all analysis narratives into a single Transient Vector Memory (TVM) store.
    This allows the RAG Q&A system to query and compare across all tickers in the batch.

    Use:
        python marketflow_batch_analysis.py AAPL MSFT GOOG
    """
    import argparse
    import os
    from datetime import datetime

    # We will modify run_analysis to be importable

    from marketflow_analysis import run_analysis, embed_fn
    from marketflow.transient_vector_memory import TransientVectorMemory
    from marketflow.marketflow_config_manager import create_app_config
    from marketflow.marketflow_logger import get_logger
    from marketflow.marketflow_utils import sanitize_filename

    def main():
        parser = argparse.ArgumentParser(description="Run batch Marketflow analysis for multiple tickers.")
        parser.add_argument("tickers", nargs='+', help="List of ticker symbols (e.g., AAPL MSFT GOOG)")
        args = parser.parse_args()

        logger = get_logger("marketflow_batch_analysis")
        config = create_app_config()
        report_root = config.REPORT_DIR

        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 1. Define a single, shared namespace for the entire batch
        namespace = f"batch:{run_id}"
        logger.info(f"Starting batch analysis. TVM Namespace: '{namespace}'")

        # 2. Initialize one TVM for the whole batch
        tvm = TransientVectorMemory(embed_fn=embed_fn, dim=1536, ttl_seconds=48*3600)

        # Prepare the directory for this batch run's consolidated TVM store
        # The Q&A app will find this by looking for the most recent .tvm_namespace file
        batch_output_dir = os.path.join(report_root, f"batch_{run_id}")
        os.makedirs(batch_output_dir, exist_ok=True)

        # 3. Loop through tickers and process them
        for ticker in args.tickers:
            logger.info(f"--- Processing ticker: {ticker} ---")
            try:
                # We will modify run_analysis to return the narrative text
                narrative, ticker_output_dir = run_analysis(ticker)

                if narrative:
                    logger.info(f"Upserting narrative for {ticker} into shared namespace.")
                    # 4. Upsert the narrative with the ticker in the metadata
                    tvm.upsert_text(
                        namespace=namespace,
                        report_id=f"{sanitize_filename(ticker)}_{run_id}",
                        text=narrative,
                        meta={"source": "marketflow_analysis", "ticker": ticker}
                    )
                else:
                    logger.warning(f"No narrative generated for {ticker}. Skipping TVM upsert.")

            except Exception as e:
                logger.error(f"Failed to process ticker {ticker}: {e}", exc_info=True)
                continue
        
        logger.info("--- Batch processing complete. Saving consolidated TVM store. ---")

        # 5. Save the consolidated TVM store and the namespace file
        tvm_dir = os.path.join(batch_output_dir, ".tvm_store")
        tvm.save_namespace(namespace, tvm_dir)

        ns_file = os.path.join(batch_output_dir, ".tvm_namespace")
        with open(ns_file, "w", encoding="utf-8") as f:
            f.write(namespace)
        
        logger.info(f"Successfully saved TVM data to {tvm_dir}")
        logger.info(f"Namespace '{namespace}' written to {ns_file}")
        print(f"\n✅ Batch analysis complete. Consolidated report data saved in {batch_output_dir}")

    if __name__ == "__main__":
        main()
    ```

### Step 2: Modify `marketflow_analysis.py`

We need to refactor `run_analysis` so it can be called as a function from our new batch script. It should now **return the narrative text and its output directory** instead of handling the TVM logic itself.

**File: `marketflow_analysis.py` (Modified)**

    ```python
    # ... (keep all imports and helper functions like CustomJSONEncoder, safe_json_dump, etc.)
    """"
    Marketflow Analysis Script
    This script runs a market analysis for a given ticker symbol using the MarketflowFacade.
    It generates reports and saves them in the specified output directory.

    Use (for single runs):
        python marketflow_analysis.py AAPL

    Use (as a module for batch processing):
        from marketflow_analysis import run_analysis
    """
    # ... (imports remain the same)
    from marketflow_facade import MarketflowFacade
    from marketflow_results_extractor import MarketflowResultExtractor
    from marketflow_report import MarketflowReport
    from marketflow_llm_interface import MarketflowLLMInterface
    from marketflow_config_manager import create_app_config
    from marketflow_logger import get_logger
    from marketflow_utils import sanitize_filename
    from marketflow_utils import save_timeframe_data
    from marketflow.transient_vector_memory import TransientVectorMemory
    from rag.embedder import embed_text

    # ... (CustomJSONEncoder, safe_json_dump, build_narrative, _compose_richer_narrative remain the same)

    def embed_fn(text: str):
        return embed_text(text)  # 1536-dim for text-embedding-3-small

    # ... (build_narrative and _compose_richer_narrative functions remain exactly the same)

    def run_analysis(ticker, timeframes=None):
        """
        Run market analysis for a given ticker symbol.
        This function now returns the generated narrative and the output directory path.
        The TVM logic is handled by the calling script (e.g., a batch processor).

        Args:
            ticker (str): Ticker symbol (e.g., AAPL or X:BTCUSD)
            timeframes (list, optional): List of timeframes to analyze.

        Returns:
            tuple[str, str]: A tuple containing (narrative_text, output_directory_path)
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        logger = get_logger("marketflow_analysis") # get logger inside function
        logger.info(f"Running analysis for {ticker} on {current_date}")

        facade = MarketflowFacade()
        if timeframes:
            results = facade.analyze_ticker(ticker, timeframes=timeframes)
        else:
            results = facade.analyze_ticker(ticker)
        
        # ... (code for saving timeframe data remains the same)
        if isinstance(results, dict) and 'timeframe_analyses' in results:
            timeframe_data_to_save = results.get('timeframe_analyses', {})
            if timeframe_data_to_save:
                save_timeframe_data(ticker, timeframe_data_to_save)

        extractor = MarketflowResultExtractor({ticker: results})
        config = create_app_config()
        report_root = config.REPORT_DIR
        output_dir = f"{report_root}/{current_date}/{sanitize_filename(ticker)}"
        
        report = MarketflowReport(extractor, output_dir=output_dir)
        report.generate_all_reports_for_ticker(ticker)

        # ... (LLM interface and saving llm_analysis.json code remains the same)
        try:
            llm_interface = MarketflowLLMInterface()
            llm_interface_analysis = llm_interface.get_ticker_analysis(ticker, analysis=results, timeframes=timeframes)
        except Exception as e:
            logger.error(f"Error creating LLM interface or getting analysis: {e}")
            llm_interface_analysis = {} # Use empty dict on failure
        
        llm_analysis_file = os.path.join(output_dir, f"{sanitize_filename(ticker)}_llm_analysis.json")
        os.makedirs(output_dir, exist_ok=True)
        safe_json_dump(llm_interface_analysis, llm_analysis_file)

        # Build the narrative
        narrative = build_narrative(output_dir, ticker, extractor)
        if not isinstance(narrative, str) or len(narrative.split()) < 15:
            logger.warning("Narrative too short/invalid; constructing richer fallback.")
            narrative = _compose_richer_narrative(ticker, llm_interface_analysis, extractor, results)
        
        if len(narrative.split()) < 8:
            narrative = f"{ticker}: Analysis summary unavailable; minimal fallback narrative."
            logger.warning(f"Using minimal fallback narrative for {ticker}")

        # REMOVED TVM LOGIC FROM HERE
        # The calling script (e.g., marketflow_batch_analysis.py) is now responsible for TVM.

        logger.info(f"Analysis for {ticker} complete. Narrative generated.")
        print(f"✅ Reports for {ticker} saved in {output_dir}")
        
        # Return the narrative and the output path
        return narrative, output_dir
                
    if __name__ == "__main__":
        # This block allows the script to still be run for a single ticker for testing/debugging.
        # It will create its own single-ticker TVM store.
        parser = argparse.ArgumentParser(description="Run Marketflow analysis for a single ticker.")
        parser.add_argument("ticker", type=str, help="Ticker symbol (e.g., AAPL or X:BTCUSD)")
        parser.add_argument("--timeframes", type=str, nargs="*", default=None,
                            help="List of timeframes (e.g., 1d 4h 1h).")
        args = parser.parse_args()

        narrative, output_dir = run_analysis(args.ticker, timeframes=args.timeframes)

        # --- Standalone TVM Creation for single run ---
        if narrative:
            run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            namespace = f"single:{sanitize_filename(args.ticker)}:{run_id}"
            logger = get_logger("marketflow_analysis_standalone")
            logger.info(f"Standalone run: Creating TVM namespace: {namespace}")
            
            tvm = TransientVectorMemory(embed_fn=embed_fn, dim=1536)
            tvm.upsert_text(
                namespace=namespace,
                report_id=f"{sanitize_filename(args.ticker)}_{run_id}",
                text=narrative,
                meta={"source": "marketflow_analysis", "ticker": args.ticker}
            )
            
            # Save TVM and namespace file in the ticker's output directory
            tvm_dir = os.path.join(output_dir, ".tvm_store")
            tvm.save_namespace(namespace, tvm_dir)
            ns_file = os.path.join(output_dir, ".tvm_namespace")
            with open(ns_file, "w", encoding="utf-8") as f:
                f.write(namespace)
            logger.info(f"Standalone TVM store for {args.ticker} saved in {output_dir}")

    ```

### Step 3: Modify `ai_studio_code.py`

Finally, update the Q&A app. It needs to query the TVM for *any* question, not just when a specific `namespace_ticker` is mentioned. The query itself will contain the ticker name, which is how the retrieval will find the right information from the consolidated vector store.

**File: `ai_studio_code.py` (Modified)**

    ```python
    # ... (imports remain the same)

    class EnhancedRAGQA:
        # ... (__init__ remains mostly the same)
        def __init__(self, session_id: str, model: str = None):
            """
            Initialize the EnhancedRAGQA class for a specific session.
            """
            self.logger = get_logger(f"EnhancedRAGQA_{session_id}")
            self.session_id = session_id
            # ... (config, memory manager, model init remains the same)
            self.config_manager = create_app_config(logger=self.logger)
            memory_file = f".marketflow/memory/session_{self.session_id}.json"
            self.memory_manager = MemoryManager(memory_file=memory_file)
            self.model = model or self.config_manager.get_llm_model()
            if not self.model:
                raise ValueError("No LLM model configured.")
            self.logger.info(f"Initialized RAG QA for session '{self.session_id}' using model '{self.model}'")

            self.ticker_extractor = TickerExtractor()
            
            self.dim = 1536
            self.tvm = TransientVectorMemory(embed_fn=embed_query, dim=self.dim, ttl_seconds=48*3600)
            
            self.namespace = None
            # self.namespace_ticker is no longer reliable as the primary identifier
            # We will use it just for display purposes if available
            self.display_name = "Recent Analysis" 
            self._load_latest_tvm_namespace()

            # ... (System prompt setup remains the same)
            if not self.memory_manager.system_messages:
                system_prompt = (
                    "You are an expert financial assistant specializing in the Wyckoff method and "
                    "Volume Price Analysis (VPA). Your answers should be clear, concise, and directly based on the provided context. "
                    "Prioritize the 'RECENT ANALYSIS' section for ticker-specific questions. "
                    "Use the 'GENERAL KNOWLEDGE' section for definitions and principles. "
                    "Cite your sources using [Source: Recent Analysis] and [Source: Knowledge Base]."
                )
                self.memory_manager.add_system_message(system_prompt)

        def _load_latest_tvm_namespace(self):
            """Finds and loads the most recent TVM namespace file created by the analysis script."""
            report_root = self.config_manager.REPORT_DIR
            # This logic correctly finds the latest namespace file, whether it's from a batch or single run
            candidates = glob.glob(os.path.join(report_root, "**", ".tvm_namespace"), recursive=True)
            if candidates:
                latest_ns_file = max(candidates, key=os.path.getmtime)
                ns_file_dir = os.path.dirname(latest_ns_file)
                tvm_dir = os.path.join(ns_file_dir, ".tvm_store")

                with open(latest_ns_file, "r", encoding="utf-8") as f:
                    ns = f.read().strip()

                loaded = self.tvm.load_namespace(namespace=ns, dirpath=tvm_dir)
                if not loaded:
                    self.logger.error(f"Found namespace file for '{ns}' but failed to load data from {tvm_dir}.")
                    return
                
                self.namespace = ns
                # Update display name based on namespace type
                if ns.startswith("batch:"):
                    self.display_name = f"Batch Analysis ({ns.split(':')[1]})"
                else:
                    try:
                        self.display_name = f"Single Analysis ({ns.split(':')[-1]})"
                    except IndexError:
                        self.display_name = "Recent Analysis"
                
                self.logger.info(f"Successfully loaded TVM namespace '{self.namespace}' ({self.display_name}).")
            else:
                self.logger.warning("No .tvm_namespace file found. Recent analysis retrieval will be disabled.")
        
        # ... (get_recent_history, _format_sources remain the same)
        
        def _format_context(self, tvm_chunks: List[Dict], chroma_chunks: List[Dict]) -> str:
            """Formats the retrieved chunks from both sources into a single context string for the LLM."""
            context_parts = []
            
            if tvm_chunks:
                # Use the display name we set during loading
                header = f"--- RECENT ANALYSIS ({self.display_name}) ---"
                tvm_content_lines = []
                for chunk in tvm_chunks:
                    # Add the specific ticker from metadata to each chunk's context
                    ticker = chunk.get('metadata', {}).get('ticker', 'Unknown Ticker')
                    tvm_content_lines.append(f"[Source: Recent Analysis for {ticker}]\n{chunk['text']}")
                
                context_parts.append(f"{header}\n" + "\n\n".join(tvm_content_lines))

            if chroma_chunks:
                chroma_content = "\n\n".join(
                    f"[Source: Knowledge Base - {chunk.get('metadata', {}).get('source', 'Unknown')}]\n{chunk['text']}" 
                    for chunk in chroma_chunks
                )
                context_parts.append(f"--- GENERAL KNOWLEDGE ---\n{chroma_content}")

            if not context_parts:
                return "No context found."

            return "\n\n".join(context_parts)

        def answer_question(self, question: str) -> str:
            """
            Processes a user question through the dual-source RAG pipeline.
            """
            self.memory_manager.add_message(
                role="user", content=question, timestamp=datetime.datetime.now().isoformat()
            )
            self.logger.info(f"Received user question: {question}")
            
            tvm_chunks = []
            # **MODIFIED LOGIC**: Always query TVM if a namespace is loaded.
            # The query text itself will handle retrieving the correct ticker's data.
            if self.namespace:
                self.logger.info(f"Querying TVM namespace '{self.namespace}' for recent analysis.")
                tvm_chunks = self.tvm.query(self.namespace, question, top_k=4)
                self.logger.info(f"Retrieved {len(tvm_chunks)} chunks from TVM.")
            else:
                self.logger.info("No TVM namespace loaded, skipping recent analysis retrieval.")

            # Always retrieve from the static knowledge base for general context
            self.logger.info("Querying ChromaDB for general knowledge.")
            chroma_chunks = chroma_retrieve_top_chunks(question, top_k=3)
            self.logger.info(f"Retrieved {len(chroma_chunks)} chunks from ChromaDB.")

            if not tvm_chunks and not chroma_chunks:
                self.logger.warning("No relevant chunks found from any source.")
                return "Sorry, I couldn't find any relevant information to answer your question."

            # ... (The rest of the function: augment prompt, call OpenAI, store response)
            # This part remains the same.
            context = self._format_context(tvm_chunks, chroma_chunks)
            history = self.get_recent_history(n=5)
            augmented_prompt = (
                "Please answer the question based on the conversation history and the context provided below.\n\n"
                f"--- CONTEXT ---\n{context}\n\n"
                f"--- QUESTION ---\n{question}"
            )
            messages_for_api = history + [{"role": "user", "content": augmented_prompt}]
            try:
                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model=self.model, messages=messages_for_api, max_tokens=1024, temperature=0.5,
                )
                answer = response.choices[0].message.content.strip()
                self.logger.info("Successfully generated answer from OpenAI.")
            except Exception as e:
                self.logger.error(f"Error during OpenAI API call: {e}", exc_info=True)
                answer = "I'm sorry, but I encountered an error while generating a response."

            if answer:
                self.memory_manager.add_message(
                    role="assistant", content=answer, timestamp=datetime.datetime.now().isoformat()
                )
            return answer

    # ... (main function remains the same)
    ```

### How to Use the New Workflow

    1.  **Run the Batch Analysis:** Open your terminal and run the new batch script with the tickers you want to analyze.

        ```bash
        python marketflow_batch_analysis.py AAPL GOOG OKLO NVDA
        ```

        This will create a new directory in your reports folder (e.g., `.marketflow/reports/batch_20231027_153000`) containing the consolidated `.tvm_store` and `.tvm_namespace` files.

    2.  **Start the Q&A Session:** Now, run your interactive Q&A script as usual.

        ```bash
        python ai_studio_code.py
        ```

        It will automatically find and load the latest TVM store, which is the consolidated one from your batch run.

    3.  **Ask Comparative Questions:** You can now ask questions about any ticker from the batch, or even ask it to compare them.

    *   `You: What is the recent analysis for GOOG?`
    *   `You: Can you summarize the key signals for OKLO?`
    *   `You: Compare the risk assessment for AAPL and NVDA.`

The RAG system will now retrieve the relevant chunks for each ticker from the single vector store and provide comprehensive, multi-ticker aware answers.
