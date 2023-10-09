if test -f "/var/www/html/sd/.lock"; then
	echo "processing is still running."
else
	echo "starting" > "/var/www/html/sd/.lock";

	echo "output: /var/www/html/sd/$1.png";
	echo "pos-prompt: $2";
	echo "neg-prompt: $3";
	echo "steps: $4";

	echo "./sd6 --xl --output \"/var/www/html/sd/$1\" --prompt \"$2\" --neg-prompt \"$3\" --steps $4 --rpi" > "/var/www/html/sd/command.txt"

	cd /

	cd media
	cd thomace
	cd EXT
	cd stable-diffusion-xl-base-1.0-onnxstream


	./sd6 --xl --output "/var/www/html/sd/$1" --prompt "$2" --neg-prompt "$3" --steps $4 --rpi

	rm "/var/www/html/sd/.lock";
	echo "Done"
fi

