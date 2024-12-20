# production and debug
alias upd='docker compose -f .gci/docker-compose.yml  -p msa_dhondt up -d --build dhondt'
alias upd_dev='docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -p msa_dhondt up -d --build dhondt'

alias downd='docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-testing.yml  -p msa_dhondt down -v'
alias drest='downd && upd'
alias drest_dev='downd && upd_dev'
alias log='docker logs msa_dhondt-dhondt-1'
alias rest='drest'
alias dod='downd'

# up/down prod container only as a service
alias posup='docker compose -f .gci/docker-compose.yml -p msa_dhondt up -d '
alias posd='docker compose -f .gci/docker-compose.yml -p msa_dhondt down -v'

# up/down database container only as a service
alias flup='docker run -it --rm -v $PWD:$PWD -w $PWD $DOCKER_EXTRA_CMD -v ${HOME}/.bash_history:/root/.bash_history -p "5000:5000" --network host --name flak_pru fl_pru bash'
alias fldow='docker stop flak_pru'

#unit tests
alias upd_unit_test='docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p msa_dhondt up -d --build dhondt unit_testing '
alias drest_unit_testing='downd && upd_unit_test'
alias execute_unit_testing='dod; upd_unit_test; sleep 2; watch -n1 docker logs msa_dhondt-unit_testing-1'

#ci tests
alias bkp_data='dod && FOLDER_BKP=db_data/$(date +%Y%m%d_%H%M%S) && mkdir -p $FOLDER_BKP &&  sudo cp -R $(docker volume inspect data_postgres | jq ".[0][\"Mountpoint\"]" | tr -d \") $FOLDER_BKP && sudo chown -R $USER:$USER $FOLDER_BKP' 
alias restore_last_data='FOLDER_DEST=$(docker volume inspect data_postgres | jq ".[0][\"Mountpoint\"]" | tr -d \") ;AUX=$(ls -td db_data/* | head -n 1 | sed "s|$|/*|"); FOLDER_BKP=$(ls -d $AUX); echo "Copying $FOLDER_BKP"; dod && sudo rm -rf $FOLDER_DEST && sudo cp -R $FOLDER_BKP $FOLDER_DEST' 
alias clear_db='dod; docker volume rm data_postgres && docker volume create data_postgres && drest_dev'

alias upd_ci_testing='docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml -p msa_dhondt up -d --build dhondt ci_testing'
alias drest_ci_testing='downd && upd_ci_testing'

alias manual_execution_ci_tests='upd_ci_testing;docker run --rm  --network host --name testing_dhondt msa_dhondt-dhondt bash -c "YAML=\$(pip show dhondt-method | grep Location | cut -d\   -f2); schemathesis run \$YAML/dhondt/web/dhondt.yaml --base-url=http://localhost:5000/dhondt/v1  --hypothesis-database=none --output-truncate=false --validate-schema=true --checks=all"'
alias execute_ci_testing='dod; upd_ci_testing && sleep 2 && watch -n1 docker logs msa_dhondt-ci_testing-1'

# documentation
alias build_doc='docker compose -f .gci/docker-compose-doc.yml  -p msa_dhondt-doc up  --build doc'
