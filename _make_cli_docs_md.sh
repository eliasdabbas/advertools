#!/usr/bin/env bash

advertools --help > adv_help

adv_commands=$(
  sed -n '/{.*}/p' adv_help \
  | head -n 1 \
  | sed 's/,/ /g' \
  | sed 's/[}{]//g'
)

for command in $adv_commands
do
    advertools "$command" --help > "$command.txt"

    title=$(
      sed '1,/^$/d' "$command.txt" \
      | head -n 1
    )

    echo "## $title"
    echo

    usage=$(
      sed '/══/d' "$command.txt" \
      | sed '/full documentation at.*/d'
    )

    echo "\`\`\`bash"
    echo "$usage"
    echo "\`\`\`"
    echo

    rm "$command.txt"
done
rm adv_help