# split_csv_polars.py
import io
import polars as pl
from typing import Optional, Dict


def split_csv_polars(
    infile: str,
    out_prefix: str,
    rows_per_file: int = 100_000,
    encoding: str = "utf-8",
    dtypes: Optional[Dict[str, pl.DataType]] = None,
    keep_header_in_each_file: bool = True,
):
    """
    Split a large CSV into multiple CSVs using Polars for parsing/writing.

    Args:
      infile: input CSV path
      out_prefix: output files will be "{out_prefix}_{idx:03d}.csv"
      rows_per_file: data rows per output file (not counting header)
      encoding: file encoding
      dtypes: optional dict mapping column name -> polars.DataType to avoid inference
      keep_header_in_each_file: write header row to every split
    """
    file_idx = 0
    buffer_lines = []
    header_line = None
    data_lines_seen = 0

    with open(infile, "r", encoding=encoding, newline="") as f:
        # read header
        header_line = f.readline()
        if not header_line:
            return  # empty file

        # normalize header line (remove trailing newline; we'll add it later)
        header_line = header_line.rstrip("\n\r")

        for line in f:
            buffer_lines.append(line.rstrip("\n\r"))
            data_lines_seen += 1

            if data_lines_seen >= rows_per_file:
                file_idx += 1
                out_path = f"{out_prefix}_{file_idx:03d}.csv"
                _write_chunk_polars(
                    header_line,
                    buffer_lines,
                    out_path,
                    encoding=encoding,
                    dtypes=dtypes,
                    keep_header=keep_header_in_each_file,
                )
                buffer_lines = []
                data_lines_seen = 0

        # last partial chunk
        if buffer_lines:
            file_idx += 1
            out_path = f"{out_prefix}_{file_idx:03d}.csv"
            _write_chunk_polars(
                header_line,
                buffer_lines,
                out_path,
                encoding=encoding,
                dtypes=dtypes,
                keep_header=keep_header_in_each_file,
            )


def _write_chunk_polars(
    header_line: str,
    data_lines: list,
    out_path: str,
    encoding: str = "utf-8",
    dtypes: Optional[Dict[str, pl.DataType]] = None,
    keep_header: bool = True,
):
    """
    Helper: create an in-memory CSV (header + data_lines), parse with Polars,
    and write to out_path.
    """
    # Join header + data into bytes buffer
    if keep_header:
        csv_text = header_line + "\n" + "\n".join(data_lines) + "\n"
    else:
        csv_text = "\n".join(data_lines) + "\n"

    buf = io.BytesIO(csv_text.encode(encoding))

    # Parse with Polars. Use provided dtypes to bypass inference when available.
    if dtypes:
        df = pl.read_csv(buf, has_header=keep_header, dtype=dtypes)
    else:
        df = pl.read_csv(buf, has_header=keep_header)

    # Write chunk to CSV (Polars uses fast writer)
    df.write_csv(out_path)


def main() -> None:
    print("Hello from split-sheet!")
    print("test")


if __name__ == "__main__":
    main()
