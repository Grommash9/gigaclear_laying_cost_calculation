
# Gigaclear Laying Cost Calculation

Project what can help gigaclear company choose parther to install their network by project budget calcualtion.

Main logic of calcualtion is inside main.py file, also we have visualizer.py script for create images form your graphml files (for test and fun porpose)

And these logic is realized as api application for easy connect it to any other serivce what we need.




## API Reference

#### Get cost information for your network configuration

```http
  POST /upload
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file` | `graphml` | **Required**. Your graphml data file |

#### Get item


## Demo

You can try it on

https://gigaclear.blockchain-callback.com/docs


## Deployment

To deploy this project run

```bash
  docker build -t gigaclear_laying_cost_calculation .

```

```bash
  docker run -p 2000:2000 gigaclear_laying_cost_calculation
```


## Roadmap

- Revoke api file processing to async

- Create callback system for not waiting for large file processing

- Logic for change card prices (add new or edit old ones)


