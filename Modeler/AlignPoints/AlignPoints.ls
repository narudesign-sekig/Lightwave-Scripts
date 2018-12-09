@warnings
@version 2.1

main
{
	x_align = recall("x", false);
	y_align = recall("y", false);
	z_align = recall("z", false);
	
	n_of_p = editbegin();
	if (n_of_p == 0) {
		error("Current layer is empty!");
		return;
	}
	editend();
	
	selmode(USER);
	
	reqbegin("AlignPoints1.00 (c)2001,SEKI");
	reqsize(208, 70);
	
	c1 = ctlcheckbox("X", x_align);
	ctlposition(c1, 20, 10);
	
	c2 = ctlcheckbox("Y", y_align);
	ctlposition(c2, 90, 10);
	
	c3 = ctlcheckbox("Z", z_align);
	ctlposition(c3, 160, 10);
	
	if(reqpost()) {
	    x_align = getvalue(c1);
    	y_align = getvalue(c2);
	    z_align = getvalue(c3);
		
		n_of_p = editbegin();
		base_point = pointinfo(points[1]);
		for (i = 1; i <= n_of_p; i++) {
			target_point = pointinfo(points[i]);
			if(x_align == true) {
				target_point.x = base_point.x;
			}
			if(y_align == true) {
				target_point.y = base_point.y;
			}
			if(z_align == true) {
				target_point.z = base_point.z;
			}
			pointmove(points[i], target_point.x, target_point.y, target_point.z);
		}
		editend();
	    
    	store("x", x_align);
	    store("y", y_align);
    	store("z", z_align);
    }
}
