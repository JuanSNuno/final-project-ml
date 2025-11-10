@echo off
cd /d "C:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml"
python -m streamlit run "C:\Users\jsanc\OneDrive\Documentos\U\ML\final-project-ml\mlops_pipeline\src\scripts\streamlit_app.py" --server.port 8502 --server.address localhost
pause
