<?php

include "project.php";
include "config.php";

$proj = new Project();

$proj->load();
	
if (! $proj->save($_POST['project'], $_POST['pos-prompt'], $_POST['neg-prompt'], $_POST['steps'], time(), false, $_POST['sdxl'])){
	print "nothing to process";
	die;		
}

if ($_POST['action'] == "SAVE PROJECT"){
	header("Content-Length: " . filesize("project.txt"));
	header('Content-Disposition: attachment; filename="' . $proj->name . '.txt"');
	
	readfile("project.txt");

	die;	
}

if ($_POST['action'] == "REFINE PROJECT"){
	if (! $proj->save($_POST['project'], $_POST['pos-prompt'], $_POST['neg-prompt'], $_POST['steps'], time(), true, $_POST['sdxl'])){
		print "nothing to process";
		die;		
	}	
}

if ($_POST['action'] == "REFINE PROJECT DROP IMAGE"){
	delete($proj->picture);
	
	if (! $proj->save($_POST['project'], $_POST['pos-prompt'], $_POST['neg-prompt'], $_POST['steps'], time(), true, $_POST['sdxl'])){
		print "nothing to process";
		die;		
	}	
}

if (substr_count($_POST['action'], "DELETE:") > 0){
	if (substr_count($_POST['action'], "snail") or 
		substr_count($_POST['action'], "rocket")){
		die;
	}
	
	//file_put_contents("test.txt", trim(str_replace("DELETE:", "", $_POST['action'])));
	
	delete(trim(str_replace("DELETE:", "", $_POST['action'])));
	die;
}




?>


<!DOCTYPE html>

<?php

if (! $_POST['pos-prompt']){
	print "nothing to process";
	die;
}


$sd_path = $sd;
$additional_parameter = ""; //none

if ($proj->sdxl > 0){
	$sd_path = $sdxl;
	$additional_parameter = "--xl";
}

//only on linux... windows coming soon
exec(sprintf('%s > /dev/null 2>&1 &', $sd_shellscript . ' "' . $proj->picture . '" "' . $proj->posprompt . '" "' . $proj->negprompt . '" ' . $proj->steps . ' "' . $sd_path . '" ' . $additional_parameter));


?>
