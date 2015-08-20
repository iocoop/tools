#!/bin/bash

USERS=( "bill:Bill Broadley:spikebike" 
        "troy:Troy Arnold:xytroyxy"
        "ben:Ben Kochie:SuperQ"
        "max:Max Baker:maxslug"
        "devin:Devin Carraway:aqua"
        "gene:Gene Wood:gene1wood"
        "gary:Gary Peck:garyp"
        "chris:Chris Haumesser:wryfi"
        "kevin:Kevin Bullock:krbullock"
        "mark:Mark Burdett:mfb"
        "tim:Tim Pepper:tpepper"
        "sarah:Sarah E. E. Burt:seeb" )

for user in "${USERS[@]}"; do
    stack="${user}"
    username="${stack%%:*}"
    stack="${stack#*:}"
    fullname="${stack%%:*}"
    stack="${stack#*:}"
    githubname="${stack%%:*}"
    if ! id ${username} >/dev/null 2>&1; then
        useradd --comment "${fullname}" --groups admin,sudo --create-home --shell /bin/bash ${username}
        id ${username}
        homedir="`getent passwd ${username} | cut --delimiter=: --fields=6`"
        group="`getent passwd ${username} | cut --delimiter=: --fields=4`"
        install --group=${group} --owner=${username} --mode=0700 --directory "${homedir}/.ssh"
        if [ ! -s "${homedir}/.ssh/authorized_keys" ]; then
            install --group=${group} --owner=${username} --mode=0600 --no-target-directory /dev/null "${homedir}/.ssh/authorized_keys"
            curl --silent --output "${homedir}/.ssh/authorized_keys" https://github.com/${githubname}.keys
            echo "Created \"${homedir}/.ssh/authorized_keys\""
        else
            echo "ERROR : Found existing \"${homedir}/.ssh/authorized_keys\" file"
        fi
    else
        echo "${username} already exists"
    fi
done