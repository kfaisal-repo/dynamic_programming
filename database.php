<?php
$servername = "localhost";
$username = "root";
$password = "";
$db_name="planner1";

// Create connection
$conn = new mysqli($servername, $username, $password,$db_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully";

################################################################# Get number of script from cbr_detail #################################
$array_contain_script=array();

$sql_get_rel = "SELECT releasestring FROM active_releases";
$result_get_rel=mysqli_query($conn,$sql_get_rel);
$output_get_relname= mysqli_fetch_all($result_get_rel,MYSQLI_ASSOC);
$arrlength_relname=count($output_get_relname);


################################

$sql_get_id_and_rel = "SELECT id,relname FROM cbr_master";
$result_get_id_and_rel=mysqli_query($conn,$sql_get_id_and_rel);
$output_get_id_and_rel= mysqli_fetch_all($result_get_id_and_rel,MYSQLI_ASSOC);
$arrlength_id_rel=count($output_get_id_and_rel);

for($x = 0; $x < $arrlength_relname; $x++) {
	for($y = 0; $y < $arrlength_id_rel; $y++) {

		if(strcmp($output_get_relname[$x]['releasestring'],$output_get_id_and_rel[$y]['relname'])==0){
			//echo "FOUND ".$output_get_relname[$x]['releasestring']."----".$output_get_id_and_rel[$y]['id'];
			$found_id_rel[$output_get_id_and_rel[$y]['id']]=$output_get_id_and_rel[$y]['relname'];
		}
	}
}

$arrlength_found = count($found_id_rel);

foreach ($found_id_rel as $key => $value) {

	$sql_get_detail_table = "SELECT pr_scen_out FROM cbr_detail WHERE master_id=$key";
	$result_get_table=mysqli_query($conn,$sql_get_detail_table);
	$output_get_table= mysqli_fetch_all($result_get_table,MYSQLI_ASSOC);
	$arrlength_blobs=count($output_get_table);
	//echo "--length--".$arrlength_blobs;
	$final_scenario_list=array();

	if(!($arrlength_blobs==0)){
		for($x = 0; $x < $arrlength_blobs; $x++) {
			 
			//echo "FFFF-- $arrlength_blobs --".$output_get_table[$x]['pr_scen_out'];
			$str_arr = preg_split ("/[\,\n]/", $output_get_table[$x]['pr_scen_out']);
			for($s = 1; $s < count($str_arr); $s=$s+3) {
				//echo "<br>".$s."#".$str_arr[$s];
				if(!in_array($str_arr[$s], $final_scenario_list)){
					array_push($final_scenario_list,$str_arr[$s]);
				}
			}
		}
		//echo "--count---".count($final_scenario_list)."----<br><br><br>";
		$array_contain_script[$found_id_rel[$key]]=count($final_scenario_list);
	}
	else{
		//echo "--ZERO length-";
	}

}


################################################################# Get number of PR per release ################################

$sql_get_PR = "SELECT relname,prs FROM cbr_master";

$result_get_PR=mysqli_query($conn,$sql_get_PR);

// Fetch all
$output_get_PR= mysqli_fetch_all($result_get_PR,MYSQLI_ASSOC);

$arrlength = count($output_get_PR);
$all_releases=array();

for($x = 0; $x < $arrlength; $x++) {
	
	$cnt_prs=preg_split("/\n/", $output_get_PR[$x]['prs']);
	
	$all_releases[$output_get_PR[$x]['relname']]=count($cnt_prs);
	//echo count($cnt_prs);
	//echo "<br>";
}

################################################################# Get release, bdp,bpp from active_releases #############################
$arrlength =0;

$sql1 = "SELECT releasestring,build_planned,deploy_planned FROM active_releases";

$result=mysqli_query($conn,$sql1);

// Fetch all
$output= mysqli_fetch_all($result,MYSQLI_ASSOC);

$arrlength = count($output);
################################################################# final push to assoc array for generating json #######################

$var;
$full_var=array();
$my_ar;

for($x = 0; $x < $arrlength; $x++) {
	$var['name']=$output[$x]['releasestring'];
	$var['bpd'] = $output[$x]['build_planned'];
	$var['bdd'] = $output[$x]['deploy_planned'];
	$var['sanity'] = 0;
	$var['tbr'] = 0;
	$var['fdt'] = 0;
	$var['full'] = 0;
	$var['priority'] = $x + 1;

	foreach ($all_releases as $key_relname => $value_prs) {
		if(strcmp($output[$x]['releasestring'], $key_relname)==0){
			$var['prs']=$value_prs;
		}
		else{
			$var['prs']=null;
		}
	}
	$var['testbeds'] = 99999;

	if(array_key_exists($output[$x]['releasestring'],$array_contain_script) && $array_contain_script[$output[$x]['releasestring']] != 0){
		$var['scripts']=$array_contain_script[$output[$x]['releasestring']];
	}
	else{
		$var['scripts']=null;
	}
	array_push($full_var,$var);
}

$arrayName2 = array("ROUTING::ACX", "ROUTING::BBE", "ROUTING::KERNEL & MGMT", "ROUTING::MMX", "ROUTING::RPD", "ROUTING::SERVICES", "ROUTING::TPTX", "SWITCHING::EX-LEGACY", "SWITCHING::EX-MOJITO", "SWITCHING::EX-RODNIK", "SWITCHING::EX-SUMMIT", "SWITCHING::EX2300", "SWITCHING::EX3400", "SWITCHING::EX4600", "SWITCHING::MARTINI", "SWITCHING::MARTINI-ROYALE", "SWITCHING::MOJITO-ROYALE", "SWITCHING::ONYX", "SWITCHING::PEARLS", "SWITCHING::Porter2", "SWITCHING::Porter3", "SWITCHING::QFABRIC", "SWITCHING::QFX-LAVC", "SWITCHING::QFX-OPUS", "SWITCHING::QFX10002", "SWITCHING::QFX10008/10016", "SWITCHING::QFX5200", "SWITCHING::QFX5210", "SWITCHING::XELLENT");


$my_ar['page']="schedule";
$my_ar['groups']=array(array("type"=>"reg","all_functions"=>$arrayName2,"releases"=>$full_var));

$abc=json_encode($my_ar);
echo "$abc";
mysqli_close($conn);
?>
