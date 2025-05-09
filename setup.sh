unset PYTHONPATH
# exec "$SHELL"

export PYTHONPATH="$PYTHONPATH:$(pwd)"
echo "Python path set to : $PYTHONPATH"

conda activate code