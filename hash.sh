#!/usr/local/bin/bash
DIR=$(cd $(dirname $0); pwd)
dest_dir="${DIR}/res_mapping/"
rm -rf ${dest_dir}
mkdir ${dest_dir}
cd ${DIR}
declare -A mapping
for file in `find ./res -type f \( -name '*.png' -o -name '*.plist' \)`
do
	dest=${dest_dir}
	file2=${file:2}
	md5_value=`echo -n $file2|md5`
	level1=${md5_value:0:2}
	level2=${md5_value:2}
	dest=${dest}"${level1}"

	if [ ! -d ${dest} ]; then
		mkdir ${dest}
	fi

	cp -v ${file} ${dest}
	fileNoPath=${file##.*\/}
	cd ${dest}
	mv -v ${fileNoPath} ${level2}
	cd ${DIR}
	mapping["${file2}"]=${md5_value}
	break
done


echo "var res_mapping = {" >src/mapping.js
for key in ${!mapping[@]}
do
	echo "'${key}'"" : ""'${mapping[$key]}'" >> src/mapping.js
done
echo "}" >> src/mapping.js

rm -rf res
mv res_mapping res

