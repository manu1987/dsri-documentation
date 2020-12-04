---
id: guide-publish-image
title: Publish a Docker image
---

> ⚠️ **DockerHub imposes strict pull limitations for clusters** like the DSRI (using DockerHub might result in failing to pull your images on the DSRI). 
>
> We highly recommend to **use the [GitHub Container Registry](https://docs.github.com/en/free-pro-team@latest/packages/getting-started-with-github-container-registry/about-github-container-registry) or [RedHat quay.io Container Registry](https://quay.io/) to publish public Docker images**.
>
> You can also login to DockerHub using a Secret in OpenShift to increase the pull rates limitations:
>
> ```bash
> oc create secret docker-registry docker-hub-secret --docker-server=docker.io --docker-username=your-dockerhub-username --docker-password=your-dockerhub-password --docker-email=your-dockerhub-email
> ```

## Login to Container Registries 🔑

### Login to GitHub Container Registry

Use your existing [GitHub](https://github.com) account if you have one:

1. Create a **Personal Access Token** for GitHub packages at **https://github.com/settings/tokens/new**
1. Provide a meaningful description for the token, and enable the following scopes when creating the token:
    * `write:packages`: publish container images to GitHub Container Registry
    * `delete:packages`: delete specified versions of private or public container images from GitHub Container Registry
1. You might want to store this token in a safe place, as you will not be able to retrieve it later on github.com (you can still delete it, and create a new token easily if you lose your token)
1. 👨‍💻 Log in to the GitHub Container Registry in your terminal (change `USERNAME` and `ACCESS_TOKEN` to yours):

```bash
echo "ACCESS_TOKEN" | docker login ghcr.io -u USERNAME --password-stdin
```

> See the [official GitHub documentation](https://docs.github.com/en/free-pro-team@latest/packages/using-github-packages-with-your-projects-ecosystem/configuring-docker-for-use-with-github-packages).

### Login to quay.io

1. Create an account at https://quay.io 
2. Login in your terminal (you will be asked for username and password)

```bash
docker login quay.io
```

### Login to DockerHub

1. Get a [DockerHub](https://hub.docker.com/) account at https://hub.docker.com (you most probably already have one if you installed Docker Desktop)

2. 👩‍💻 Run in your terminal:

```bash
docker login
```

3. Provide your DockerHub username and password.

## Publish your image 📢

Once you built a Docker image, and you logged in to a Container Registry, you might want to publish the image to pull and re-use it easily later.

### Publish to GitHub Container Registry

The [GitHub Container Registry](https://docs.github.com/en/free-pro-team@latest/packages/getting-started-with-github-container-registry) is still in beta but will be free for public images when fully released. It enables you to store your Docker images at the same place you keep your code! 📦

Publish to your user Container Registry on GitHub:

```bash
docker build -t ghcr.io/github-username/my-image:latest .
docker push ghcr.io/github-username/my-image:latest
```

For example, to the [MaastrichtU-IDS organization Container Registry on GitHub](https://github.com/orgs/MaastrichtU-IDS/packages):

```bash
docker build -t ghcr.io/maastrichtu-ids/jupyterlab-on-openshift:latest .
docker push ghcr.io/maastrichtu-ids/jupyterlab-on-openshift:latest
```

> If the image does not exist, GitHub Container Registry will create it automatically and set it as **Private** by default. You can easily change it to **Public** in the image settings on github.com.

### Publish to Quay.io

1. Create the image on [quay.io](https://quay.io/)

2. Build and push to [quay.io](https://quay.io/)

```bash
docker build -t ghcr.io/quay-username/my-image:latest .
docker push quay.io/quay-username/my-image:latest
```

### Publish to DockerHub

It is not recommended, but [DockerHub](https://hub.docker.com/) is still the most popular and mature Container Registry, if you are login to DockerHub on the DSRI it should allow you to pull DockerHub images in your project (see at the start of this page to do so).

1. Create the repository on [DockerHub](https://hub.docker.com/) (attached to your user or an [organization](https://hub.docker.com/orgs/umids/repositories))
2. Build and push the image:

```bash
docker build -t dockerhub-username/jupyterlab:latest .
docker push dockerhub-username/jupyterlab:latest
```

> You can also change the name (aka. tag) of an existing image:
>
> ```bash
> docker build -t my-jupyterlab .
> docker tag my-jupyterlab ghcr.io/github-username/jupyterlab:latest
> ```

### Use automated workflows

You can automate the building and publication of Docker images using GitHub Actions workflows 🔄

👀 Check the [`.github/workflows/publish-docker.yml` file](https://github.com/MaastrichtU-IDS/get-started-with-docker/blob/main/.github/workflows/publish-docker.yml) to see an example of a workflow to publish an image to the GitHub Container Registry.

👩‍💻 You only need to change the `IMAGE_NAME`, and use it in your GitHub repository to publish a Docker image for your application automatically! It will build from a `Dockerfile` at the root of the repository.

The workflow can be easily configured to:

* publish a new image to the `latest` tag at each push to the main branch
* publish an image to a new tag if a release is pushed on GitHub (using the git tag)
  * e.g. `v0.0.1` published as image `0.0.1`

> If you publish your image on DockerHub, you can use [automated build on DockerHub](https://docs.docker.com/docker-hub/builds/).

> GitHub Actions is still currently evolving quickly, feel free to check if they recommend a new way to build and publish containers 🚀