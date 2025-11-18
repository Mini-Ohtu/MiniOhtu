## Ohtu miniprojekti README

Lue [täältä](https://ohjelmistotuotanto-hy.github.io/flask/) lisää.

Muutamia vihjeitä projektin alkuun [täällä](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/blob/main/misc/ohjeita.md).

Linkki ryhmän backlogiin [tässä](https://docs.google.com/spreadsheets/d/1Gf4uw0c0myjrpMIgQNJ6P5u_mz90s6L_LBdPb7gv93k/edit?usp=sharing)

## Docker + Postgres

1. Rakenna image: `docker build -t ohtu-db .`
2. Aja kanta: `docker run --rm -p 5433:5432 ohtu-db`
3. Yhdistä: `psql postgresql://admin:admin@localhost:5433/ohtu_db`