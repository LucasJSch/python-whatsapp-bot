#!/bin/bash

# Unset TMUX variable to prevent nested tmux sessions
unset TMUX

# Define the tmux session name
SESSION_NAME="wpp_bot_tmux_session"

# Start a new tmux session in the background (without attaching to it)
tmux new-session -d -s $SESSION_NAME

# Create 2 panes (horizontal split)
tmux split-window -h -t $SESSION_NAME:0

# Start the ngrok server in the first pane (0.0)
tmux send-keys -t $SESSION_NAME:0.0 'ngrok http 8000 --domain immune-painfully-pelican.ngrok-free.app' C-m

# Start the Python script in the second pane (0.1)
tmux send-keys -t $SESSION_NAME:0.1 'python3 run.py' C-m

# Optional: Attach to the session (remove this line if you don't want to attach)
tmux attach -t $SESSION_NAME
