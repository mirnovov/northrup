import glob, os, shutil
from fontTools import ttLib

ZIP_NAME = "Northrup"

OUT_PATH = "./out/files"
JAR_PATH = "../BitsNPicas.jar"

UNITS_PER_EM = 1024
PX_SIZE = 64

os.makedirs(OUT_PATH, exist_ok = True)

for kbitx in glob.iglob("./src/*.kbitx"):
	name = os.path.basename(os.path.splitext(kbitx)[0])
	dest = f"{OUT_PATH}/{name}.ttf"
	
	if os.path.exists(dest):
		os.remove(dest)
	
	os.system(
		f"java -jar {JAR_PATH} " +
		f"convertbitmap -f ttf -w {PX_SIZE} -h {PX_SIZE} -o {dest} {kbitx}"
	)
	
	with ttLib.TTFont(dest) as font:
		font["head"].unitsPerEm = UNITS_PER_EM
		font.save(dest)
	
	os.system(f"woff2_compress {dest}")
	shutil.copyfile(kbitx, f"{OUT_PATH}/{name}.kbitx")

os.chdir(OUT_PATH)
shutil.make_archive(f"../{ZIP_NAME}", "zip")
