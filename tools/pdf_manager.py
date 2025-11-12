# pdf_manager.py
import shutil
from pathlib import Path
import subprocess  # 确保导入正确的模块名

# pdf_manager.py
def generate_pdf(latex_dir, pdf_dir, version, model_name, doc_type):
    """
    Generate PDF from LaTeX source files.

    Args:
        latex_dir (Path): Path to the directory containing LaTeX source files.
        pdf_dir (Path): Path to the directory where the generated PDF will be saved.
        version (str): Version of the document (e.g., "v1.4").
        model_name (str): Model name (e.g., "N706B").
        doc_type (str): Type of the document (e.g., "AT 命令手册").

    Returns:
        None
    """
    # Ensure that version string is formatted correctly (removing any leading 'v' or 'V')
    version_label = version.lstrip("vV").replace(".", "_")

    # Generate output PDF path
    out_pdf = pdf_dir / f"Neoway_{model_name}_{doc_type}_V{version_label}.pdf".replace(" ", "_")

    # Ensure the output directory exists
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Print the location of the generated PDF
    print(f"PDF will be saved as {out_pdf}")

    # Compile the LaTeX document using XeLaTeX
    latex_file = latex_dir / "Neoway_N706B_Manual.tex"

    # Running the XeLaTeX command to generate PDF
    try:
        subprocess.run(
            ["xelatex", "-output-directory", str(pdf_dir), str(latex_file)],
            check=True,
        )
        print(f"PDF generated successfully at {out_pdf}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during PDF generation: {e}")
        raise
