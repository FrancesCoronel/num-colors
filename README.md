# num-colors

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Given a URL of an image, this returns the number of colors in that image using image-magick.

jinageresizer is a image resizing service using flask, imagemagick and [wand](http://docs.wand-py.org/en/0.4.0/) inspired by [firesize](http://firesize.com)

---

## Current URL Scheme

`base_url/image_url/?rwidth=resize_width_in_px&rheight=resize_height&type=jpg|png`
Example:
`https://images.jinpark.net/http://i.imgur.com/AMTTUDK.jpg/?rwidth=300&type=png`

Only the image_url is required. The query params are all optional.

If width and height are given, aspect ratio is not preserved. If only width or height is given, aspect ratio is preserved and the non specified variable is modified to fit the aspect ratio.

I highly suggest putting this behind a cdn to allow for edge caching so the server is not reprocessing the same image again and again. If you are using cloudflare, as I am, you might need to force cloudflare to cache everything using page rules, since the resulting url is usually not one of the automatic cached extensions.

---

For the final project, you will be building and deploying an API that does one thing: given a URL of an image, it returns the number of colors in that image. Example implementation:

http://images.afeld.me/

The goal of this assignment is to take this (relatively) simple application, make it performant, reliable, and highly available, and sustain these things over time.

## Requirements

The URL of your API must be `images.<yourdomain>/api/num_colors?src=<imageurl>`.

For example, http://images.mysite.com/api/num_colors?src=http://othersite.com/cat.png (<-- not a working URL)

You must submit the domain name you will be using through CMS.

The app must be able to handle any common image format: JPEG, PNG, etc.

The number of colors needs to be returned as an integer as plain text...no HTML tags, JSON, additional wording, etc.

Use the following ImageMagick command to get the number of colors: `identify -format %k <filename>`

ImageMagick unfortunately seems to return slightly different answers on different machines, so it will be checked with a 5% tolerance.

The application is deployed to AWS EC2.

Use only `t2.micro` instance types.

Don’t use more than four instances for the application servers.

For a request to be considered “successful” by the scoring system, it must complete in under 15 seconds.

