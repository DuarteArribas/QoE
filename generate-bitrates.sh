#!/bin/bash

for i in {1..16};do
  ffmpeg -i images/${i}.png -q:v 100  images/${i}-1.jpg
  ffmpeg -i images/${i}.png -q:v 70   images/${i}-2.jpg
  ffmpeg -i images/${i}.png -q:v 30   images/${i}-3.jpg
  ffmpeg -i images/${i}.png -q:v 1    images/${i}-4.jpg
done