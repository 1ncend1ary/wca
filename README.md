# WCA (Web Categories Annotator)

![telegram message](https://github.com/1ncend1ary/wca/workflows/telegram%20message/badge.svg?event=push)

## ITMO University coding practice project.

#### Quick start guide:

```sh
git clone git@github.com:1ncend1ary/wca.git
cd wca
```
1. Get the `secrets.tar.gz` archive and place it in `.` [current project directory, `~/../wca/`]
2. Unarchive with:
     - `tar -xvzf secrets.tar.gz`
     - or `source bin/unarchive.sh`
3. Place pre-trained compressed `GoogleNews-vectors-negative300.bin.gz` model in `wca/web/model/`
(alternatively, use the `wca/web/model/download.sh` script)
2. Ensure [`Docker`](https://gist.github.com/1ncend1ary/1cb77bebb575ef6bfdc7c3bfb1454800) daemon is running.
3. `docker-compose up`
6. In your browser: `localhost:8080` for web application, `localhost:19981` for database web-interface.
7. You can follow [this](http://ec2-54-80-63-254.compute-1.amazonaws.com:8080/) link for a deployed application

###### [Working progress guide](./WP.md)
