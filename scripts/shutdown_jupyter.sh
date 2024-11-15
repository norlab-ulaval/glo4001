#!/usr/bin/env bash
ps aux | grep jupyter | awk '{print $2}' | xargs kill || true
