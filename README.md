# WCA (Web Categories Annotator)

![telegram message](https://github.com/1ncend1ary/wca/workflows/telegram%20message/badge.svg?event=push)

## ITMO University coding practice project.

#### Quick start guide:

```sh
git clone git@github.com:1ncend1ary/wca.git
cd wca
```
1. Place `secrets.tar.gz` archive in `.` [current project directory, `~/../wca/`]
2. Unarchive with:
     - `tar -xvzf secrets.tar.gz`
     - or `source bin/unarchive.sh`
3. Place pre-trained `GoogleNews-vectors-negative300.bin` model in `wca/web/model/` (you can use the `download.sh` script)
2. Ensure `Docker` daemon is running.
3. `docker-compose up`
6. In your browser: `localhost:8080` for web application, `localhost:19981` for database web-interface.

###### [Working progress guide](./WP.md)
