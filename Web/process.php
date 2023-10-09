<?php

include "project.php";

$proj = new Project();

$proj->load();
	
if (! $proj->save($_POST['project'], $_POST['pos-prompt'], $_POST['neg-prompt'], $_POST['steps'], time())){
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
	if (! $proj->save($_POST['project'], $_POST['pos-prompt'], $_POST['neg-prompt'], $_POST['steps'], time(), true)){
		print "nothing to process";
		die;		
	}	
}

if ($_POST['action'] == "REFINE PROJECT DROP IMAGE"){
	delete($proj->picture);
	
	if (! $proj->save($_POST['project'], $_POST['pos-prompt'], $_POST['neg-prompt'], $_POST['steps'], time(), true)){
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

/*
$targetfile = md5(time());
$targetfile .= ".png";


$_POST['pos-prompt'] = str_replace(array("
", "\r", "\n"), ", ", trim($_POST['pos-prompt']));

$_POST['neg-prompt'] = str_replace(array("
", "\r", "\n"), ", ", trim($_POST['neg-prompt']));

file_put_contents("project.txt", $_POST['project'] . "
" . $_POST['pos-prompt'] . "
" . $_POST['neg-prompt'] . "
" . $_POST['steps'] . "
" . $targetfile);

*/


//only on linux... windows coming soon
exec(sprintf('%s > /dev/null 2>&1 &', '/var/www/html/sd/sd.sh "' . $proj->picture . '" "' . $proj->posprompt . '" "' . $proj->negprompt . '" ' . $proj->steps . ''));


?>
