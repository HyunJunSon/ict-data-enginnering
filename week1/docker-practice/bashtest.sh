#!/bin/zsh
if [ -f "access2.log" ]; then
	echo "파일이 있습니다."
elif [ -d "logs" ]; then
	echo "파일은 없지만 logs 폴더는 있습니다"
else
	echo "둘 다 없습니다"
fi
