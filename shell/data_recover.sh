dd if=/dev/sdd1 bs=4096 | strings | grep -A 200 '# encoding: utf8' > re.logs
