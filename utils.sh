alias upd_dev='docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -p msa_dhondt up -d --build dhondt'
alias upd='docker compose -f .gci/docker-compose.yml  -p msa_dhondt up -d --build dhondt'

alias downd='docker compose -f .gci/docker-compose.yml -p msa_dhondt down -v'
alias drest='downd && upd'
alias drest_dev='downd && upd_dev'
alias log='docker logs msa_dhondt-dhondt-1'
alias rest='drest'
alias dod='downd'

alias posup='docker compose -f .gci/docker-compose.yml -p msa_dhondt up -d '
alias posd='docker compose -f .gci/docker-compose.yml -p msa_dhondt down -v'

alias flup='docker run -it --rm -v $PWD:$PWD -w $PWD $DOCKER_EXTRA_CMD -v ${HOME}/.bash_history:/root/.bash_history -p "5000:5000" --network host --name flak_pru fl_pru bash'
alias fldow='docker stop flak_pru'
