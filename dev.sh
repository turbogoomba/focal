#!/usr/bin/env bash
# Starter utviklingsmiljøet for focal i tmux.
# Kjør med: ./dev.sh

S=focal
DIR="$HOME/Documents/GitHub/focal"
VENV="source .venv/bin/activate"

# Finnes økten allerede, hopp rett inn i den
if ! tmux has-session -t "$S" 2>/dev/null; then
  # Vindu 1: kode i Neovim
  tmux new-session -d -s "$S" -n code -c "$DIR"
  tmux send-keys -t "$S:code" "$VENV && nvim main.py" C-m

  # Vindu 2: textual console til venstre, kjør appen til høyre
  tmux new-window -t "$S" -n run -c "$DIR"
  tmux send-keys -t "$S:run" "$VENV && textual console" C-m
  tmux split-window -h -t "$S:run" -c "$DIR"
  tmux send-keys -t "$S:run" "$VENV && clear" C-m

  # Vindu 3: git
  tmux new-window -t "$S" -n git -c "$DIR"
  tmux send-keys -t "$S:git" "git status" C-m

  tmux select-window -t "$S:code"
fi

# Inne i tmux allerede: bytt økt. Ellers: koble til.
if [ -n "$TMUX" ]; then
  tmux switch-client -t "$S"
else
  tmux attach -t "$S"
fi
