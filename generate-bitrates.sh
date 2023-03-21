#!/bin/zsh

mkdir images/JPG
mkdir images/JPG2000
mkdir images/AV1

for i in {1..5};do
  # JPEG
  for j in {0..3};do
    let bitrate=$(($j * (31 / 3) + 1))
    mkdir images/JPG/bitrate-$((4-$j)) 2> /dev/null
    ffmpeg -nostdin -y -i images/References/$i.png -pix_fmt rgb24 -q:v $bitrate images/JPG/bitrate-$((4-$j))/$i.jpg
  done
  # JPEG2000
  for j in {0..3};do
    let bitrate=$(($j * (1000 / 3) + 1))
    mkdir images/JPG2000/bitrate-$((4-$j)) 2> /dev/null
    ffmpeg -nostdin -y -i images/References/$i.png -pix_fmt rgb24 -codec jpeg2000 -frames:v 1 -q:v $bitrate images/JPG2000/bitrate-$((4-$j))/$i.jp2
    ffmpeg -nostdin -y -i images/JPG2000/bitrate-$((4-$j))/$i.jp2 -codec png -pix_fmt rgb24 images/JPG2000/bitrate-$((4-$j))/$i.png
  done
  # AV1
  for j in {0..3};do
    let bitrate=$(($j * (40 / 3) + 1))
    mkdir images/AV1/bitrate-$((4-$j)) 2> /dev/null
    ffmpeg -nostdin -y -i images/References/$i.png -c:v libx264rgb -pix_fmt rgb24 -crf $bitrate images/AV1/bitrate-$((4-$j))/$i.mp4
    ffmpeg -nostdin -y -i images/AV1/bitrate-$((4-$j))/$i.mp4 -codec png -pix_fmt rgb24 images/AV1/bitrate-$((4-$j))/$i.png
  done
done