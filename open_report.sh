#!/bin/bash

if ! command -v anywhere &> /dev/null
then
    echo "anywhere not found, installing..."
    npm install -g anywhere
fi

echo "Starting anywhere..."
anywhere