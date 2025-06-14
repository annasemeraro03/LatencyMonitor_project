# LatencyMonitor_project
## Description

LatencyMonitor_project is a tool for monitoring and analyzing the latency of systems or applications. It allows you to collect performance data, visualize statistics, and identify potential bottlenecks.

## Features

- Real-time latency monitoring
- Data collection and storage
- Graphical visualization of results
- Support for different types of input/output

## Installation

### Download the project locally

To download the project and work on it, use the following commands:

```bash
>> git clone https://github.com/annasemeraro03/LatencyMonitor_project.git
>> cd LatencyMonitor_project
```

## Requirements

Before starting the project, please do this:

```bash
>> ./setup.sh
```

or 

```bash
>> bash setup.sh
```

The script above installs the dependencies and starts a virtual environment.

## Usage

To start the django server, do this:

```bash
>> ./start.sh
```

or 

```bash
>> bash start.sh
```

This script will: 
1. make migrations
2. start an MQTT listener in background (for the home page)
3. start django server

## License

This project is licensed under the MIT License.

## Testing

There are several tests (of views and functions) in this project. To execute all the tests available do this:

```bash
>> ./tests.sh
```

or

```bash
>> bash tests.sh
```