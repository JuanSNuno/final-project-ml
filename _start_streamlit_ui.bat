@echo off
cd /d "C:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml"
python -m streamlit run "C:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml\mlops_pipeline\src\scripts\prediction_ui.py" --server.port 8501 --server.address localhost
pause
