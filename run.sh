mysh=""

if [ $1 ]; then
    mysh=$(find ~/ 2>/dev/null -type f -perm /u=x -print | grep $1 | uniq | head -n 1);
else
    mysh=$(find ~/ 2>/dev/null -type f -perm /u=x -print | grep "mysh" | uniq | head -n 1);
fi

if ! [ $mysh ]; then
    echo "Asegurate de tener compilado el binario mysh o pasarle el nombre a buscar de tu shell";
    exit 0;
fi

echo "Running $mysh"

pytest --program $mysh -v

rm a1.txt a.txt b.txt somedir -rf testdir/ __pycache__/ .pytest_cache 2>/dev/null

