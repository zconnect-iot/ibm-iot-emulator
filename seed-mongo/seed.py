#!/usr/bin/env python

"""
Seed integration overlock beta atlas:

python seed.py \
    --host 'cluster0-shard-00-00-skv03.mongodb.net,cluster0-shard-00-01-skv03.mongodb.net,cluster0-shard-00-02-skv03.mongodb.net' \
    --username integration-rw \
    --db integration \
    --ssl True \
    --rs Cluster0-shard-0 \
    --password <password in lastpass>
"""

from subprocess import check_output
import click


def wrapout(cmds):
    output = check_output(cmds)
    print(output.decode("utf8"))


@click.command()
@click.option("--host")
@click.option("--username")
@click.option("--password")
@click.option("--db")
@click.option("--rs")
@click.option("--datafile")
@click.option("--ssl", default=True, type=bool)
@click.option("--drop", default=False, type=bool)
@click.option("--collection")
def seed(host, username, password, rs, datafile, db, ssl, drop, collection):

    base = [
        "--username",
        username,
        "--password",
        password,
        "--authenticationDatabase",
        "admin",
    ]

    if ssl:
        base.append("--ssl")

    drop_cmd = [
        "mongo",
        "--host",
        "mongodb://{}?replicaSet={}".format(host, rs),
        *base,
        "--eval",
        'acl_db = db.getSiblingDB("{0}"); acl_db.{1}.drop();'.format(db, collection),
    ]

    seed_cmd = [
        "mongoimport",
        "--host",
        "{}/{}".format(rs, host),
        *base,
        "--collection",
        collection,
        "--db",
        db,
        "--type",
        "json",
        "--file",
        datafile,
        "--jsonArray",
    ]

    if drop:
        wrapout(drop_cmd)

    wrapout(seed_cmd)


if __name__ == "__main__":
    seed()
