# elastic-kibana-demo

## run `elastic` & `kibana` first

    docker-compose up

For more information check the `docker-compose.yml` file, but in simple words it spins up the following:

```
services:
    elasticsearch:
      image: docker.elastic.co/elasticsearch/elasticsearch:7.10.0
      ports:
          - '9200:9200'
          - '9300:9300'

    kibana:
      image: docker.elastic.co/kibana/kibana:7.10.0
      ports:
        - 5601:5601
```

## push some random data to `elastic`

    python3 example.py


## visualize with `kibana`

(Images are links to video files)

[![Watch the video](README/video-preview-index-pattern.jpg)](README/create_index_pattern.mp4)

[![Watch the video](README/video-preview-new-visualization.jpg)](README/create_visualization.mp4)
