# Youtube Stream - Stream live youtube streams as 10fps streams over UDP

# List of streams and format codes
stream_prefix="https://youtube.com/watch?v="
stream_ids=("YByJ2h0T5JY", "5_XSY1AfJ2M", "1EiC9bvVGnk")
formats=(95, 95, 95)
ports=(3001, 3002, 3003)

# Put together the input and output URIs
STREAM_URL=${stream_prefix}${stream_ids[$1]}
OUTPUT_URL="udp://127.0.0.1:"${ports[$1]}

# Start streaming
ffmpeg -i $(youtube-dl -f 95 -g $STREAM_URL -vf fps=10 -f mpegts $OUTPUT_URL
