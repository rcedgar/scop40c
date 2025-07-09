for x in `cat labels.txt`
do
	z=`echo $x \ | cut -d/ -f1`
	y=`echo $x | tr / _ | sed "-es/\.[0-9]*\.[0-9]*$//"`
	mv -v big_pdb/$z.pdb big_pdb/$y.pdb
done
