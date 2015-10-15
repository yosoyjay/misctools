#!/bin/bash
name=slr_1m
ssh ${ARCHIVER} "mkdir ${ARCHIVE}/$name"
find . -maxdepth 1 -type f -print0 | xargs -0 tar cvf - | ssh ${ARCHIVER} "cat > ${ARCHIVE}/$name/inputs.tar" > $name\_inputs.log
time tar cvf - combined/{1..100}_*.nc | ssh ${ARCHIVER} "cat > ${ARCHIVE}/$name/$name\_combined_1-100.tar" > $name\_1-100.log
time tar cvf - combined/{101..200}_*.nc | ssh ${ARCHIVER} "cat > ${ARCHIVE}/$name/$name\_combined_101-200.tar" > $name\_101-200.log
time tar cvf - combined/{201..300}_*.nc | ssh ${ARCHIVER} "cat > ${ARCHIVE}/$name/$name\_combined_201-300.tar" > $name\_201-300.log
time tar cvf - combined/{301..400}_*.nc | ssh ${ARCHIVER} "cat > ${ARCHIVE}/$name/$name\_combined_301-400.tar" > $name\_301-400.log
time tar cvf - combined/{401..500}_*.nc | ssh ${ARCHIVER} "cat > ${ARCHIVE}/$name/$name\_combined_401-500.tar" > $name\_401-500.log
time tar cvf - combined/{501..600}_*.nc | ssh ${ARCHIVER} "cat > ${ARCHIVE}/$name/$name\_combined_501-600.tar" > $name\_501-600.log
time tar cvf - combined/{601..700}_*.nc | ssh ${ARCHIVER} "cat > ${ARCHIVE}/$name/$name\_combined_601-700.tar" > $name\_601-700.log
time tar cvf - combined/{701..731}_*.nc | ssh ${ARCHIVER} "cat > ${ARCHIVE}/$name/$name\_combined_701-731.tar" > $name\_701-731.log
