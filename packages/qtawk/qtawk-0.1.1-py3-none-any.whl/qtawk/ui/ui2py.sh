for i in $(ls *.ui); do pyuic5 $i > $(echo $i.py | sed -e "s/\.ui\.py$/\.py/g");done
