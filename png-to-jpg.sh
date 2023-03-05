#!/bin/zsh

for i in {1..16};do
  ffmpeg -i images/$i.png images/${i}ref.jpg
done