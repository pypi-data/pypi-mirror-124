
{
  for (i=0; i < 256; i++) {
    t[sprintf("%c", i)] =sprintf("%c", i)
  }
  for (i=97; i < 97+13; i++) {
    t[sprintf("%c", i)] =sprintf("%c", i+13)
  }
  for (i=97+13; i < 97+26; i++) {
    t[sprintf("%c", i)] =sprintf("%c", i-13)
  }
  for (i=65; i < 65+13; i++) {
    t[sprintf("%c", i)] =sprintf("%c", i+13)
  }
  for (i=65+13; i < 65+26; i++) {
    t[sprintf("%c", i)] =sprintf("%c", i-13)
  }
  
  b="97,110,13,110,123,-13,65,73,13,73,91,-13"
  split(b,v,",")
   
   for (i=0; i < 256; i++) {
    t2[sprintf("%c", i)] =sprintf("%c", i)
  }

for (j=0; j<4; j++) {
	printf("%d %d %d %d\n", j, v[j * 3+1], v[j * 3+2], v[j * 3+3] )
	for (i=sprintf("%d", v[j*3+1]); i < sprintf("%d", v[j*3+2]); i++) {
		t2[sprintf("%c", i)] = sprintf("%c", i + sprintf("%d", v[j*3+3]))
		printf("%c %c\n", sprintf("%c", i), t2[sprintf("%c", i)])
	}
	printf("============\n")
}

for (i=65; i < 65+26; i++) {
    printf("%c %c\n", sprintf("%c", i), t2[sprintf("%c", i)])
  }


  split($0, chars, "")
  for (i=1; i <= length($0); i++) {
    printf("%c", t[sprintf("%c", chars[i])] )
  } 

}

