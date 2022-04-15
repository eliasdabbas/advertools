
advertools --help > adv_help

adv_commands=$(sed -n '/{.*}/p' adv_help | head -n 1 | sed 's/,/ /g' | sed 's/[}{]//g')

for command in $adv_commands
do

advertools $command --help > $command.txt

echo
title=$(cat $command.txt | sed '1,/^$/d' | head -n 1)
title_len=$(echo $title | wc -c)

echo $title
for i in $(seq 1 $title_len); do printf  = ; done
echo
echo
echo

cat $command.txt | sed '/══/d'  | sed '/full documentation at.*/d' | sed 's/^/    /' | sed -E 's/^\s+$//'

rm $command.txt

done

# dns () { for line in $(cat $1); do host $line >> $2 ; done }
# columns () { head -n 1 $1 |  sed 's/,/\n/g' | cat -n; }