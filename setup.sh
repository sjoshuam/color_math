## RUN AT THE START OF EACH SESSION

## navigate to the right directory and activate virtual environment
cd ~/code/color_math
source ~/env/color_math/bin/activate

## RUN INITIALLY TO SET UP THE ENVIRONMENT

## set up a virtual environment with the right Python packages
mkdir ~/code/color_math
cd ~/code/color_math
python3.12 -m venv ~/env/color_math
source ~/env/color_math/bin/activate
pip install --upgrade pip
pip install pandas==2.2.2 plotly==5.22.0 openpyxl==3.1.5

## configure git to ignore caches and invisible
echo ".*
io_mid/*
__pycache__" > .gitignore

## populate directory with essential files
echo '# color_math: Understanding HSV Coordinates' > README.md
cp ~/code/roadtrips/LICENSE.md ~/code/color_math/LICENSE.md

## commit directory and upload to github
git init
git add -A
git commit -m "Upload initial files"
git remote add origin git@github.com:sjoshuam/color_math.git
git branch -M main