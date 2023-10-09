<!DOCTYPE html>
<html><body>
<?php

/*if ($od = opendir("./")){
	while($rd = readdir($od)){
		if (substr_count($rd, ".lock") > 0){
			print "RUNNING";
			die;
		}
	}
}*/

//debug:
//print "robot1.png";
//die;

if (file_exists(".lock")){
	print "RUNNING";
	die;
}

/*
class Project{
	public $name;
	public $posprompt;
	public $negprompt;
	public $steps;
	public $seed;
	public $picture;
}


$data = explode("
", file_get_contents("project.txt"));
	
	$proj = new Project();
	
	if (strlen($data[0]) > 2){
		$proj->name = $data[0].trim();
		$proj->posprompt = $data[1].trim();
		$proj->negprompt = $data[2].trim();
		$proj->steps = $data[3].trim();
		$proj->picture = $data[4].trim();
		
		if (file_exists($proj->picture)){
			print $proj->picture;
			die;
		}
	}
*/

include "project.php";

$proj = new Project();

$proj->load();

if (file_exists($proj->picture)){
	print $proj->picture;
	die;
}

print "NONE";

?>
</body>
</html>
