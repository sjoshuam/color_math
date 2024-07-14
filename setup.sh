## run at the start of each session
cd ~/code/color_math
source ~/env/color_math/bin/activate

## run initially to set up virtual environment
mkdir ~/code/color_math
cd ~/code/color_math
python3.12 -m venv ~/env/color_math
source ~/env/color_math/bin/activate
pip install --upgrade pip
pip install pandas==2.2.2 plotly==5.22.0 openpyxl==3.1.5

echo ".*
io_mid/*
__pycache__" > .gitignore

git init
git add -A
git 