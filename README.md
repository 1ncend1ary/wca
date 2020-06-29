# WCA (Web Categories Annotator)

## ITMO University coding practice project.

### Quick start guide for deployment:
1. Get all the `Docker` images [here](https://github.com/1ncend1ary/wca/packages).
2. Create a directory and place the `docker-compose.yml` file there.
3. Place the `secrets.tar.gz` archive there and extract it.
4. Follow instructions in `secrets/README.txt`.
5. After all of that, run `docker-compose up`.

#### Note:
In order to get `Docker` images, you need to login to docker on your local machine. The login process is described [here](https://help.github.com/en/packages/using-github-packages-with-your-projects-ecosystem/configuring-docker-for-use-with-github-packages#authenticating-to-github-packages) 

### Quick start guide for development:

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
4. Ensure [`Docker`](https://gist.github.com/1ncend1ary/1cb77bebb575ef6bfdc7c3bfb1454800) daemon is running.
5. `docker-compose -f docker-compose.duild.yml up` to build development application.
6. In your browser: `localhost:8080` for web application, `localhost:19981` for database web-interface.
7. You can follow [this](http://ec2-54-80-63-254.compute-1.amazonaws.com:8080/) link for a deployed application

###### [Working progress guide](./WP.md)
