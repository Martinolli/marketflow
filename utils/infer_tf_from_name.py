def infer_tf_from_name(name: str) -> str | None:
        """Infer the time frame from the file name.

        This method looks for common time frame indicators in the file name
        and returns the corresponding time frame as a string.
        Parameters
        ----------
        name: str
            The name of the file from which to infer the time frame.
        Returns
        -------
        str | None
            The inferred time frame (e.g., "1d", "4h", "1h", "30m", "15m", "5m", "1m"),
            or None if no common indicators are found.
        """
        s = name.lower()
        for key in ["1d","4h","1h","30m","15m","5m","1m"]:
            if key in s: return key
        return None