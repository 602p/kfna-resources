echo Clean...
rm -rf public

echo Setup and copy static...
mkdir public
mkdir public/restaurants/
mkdir public/businesses/
cp -r static public

echo Compiling SASS...
sass sass/:public/static/scss/

echo Build restaurants...
python3 restaurant.py

echo Build businesses...
python3 business.py

echo OK