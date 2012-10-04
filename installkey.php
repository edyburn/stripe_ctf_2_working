<?php
mkdir("/mount/home/user-__________/.ssh", 0755);
copy("key.rsa.pub", "/mount/home/user-________/.ssh/authorized_keys");
chmod("/mount/home/user-_________/.ssh/authorized_keys", 0644);

echo getcwd();

?>
