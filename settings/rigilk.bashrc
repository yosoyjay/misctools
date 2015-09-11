# .bashrc file for lopezj 
#
# Source global definitions
if [ -f /etc/bashrc ]; then
. /etc/bashrc
fi

# Append history not clobber at end of sessions
shopt -s histappend
# One history, erase duplicates
export HISTCONTROL=ignoredups:erasedups
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
# More please
export HISTSIZE=10000
export HISTFILESIZE=10000

# Exports 
export SVN=/home/workspace/users/lopezj/svn
export SCRIPTS=/home/workspace/users/lopezj/scripts
export MATLAB=/home/workspace/users/lopezj/scripts/matlab
export PROJECTS=/home/workspace/project/lopezj/projects/
export SSVN=/home/workspace/users/lopezj/src/selfe_svn/trunk/src
export SEDM=/home/workspace/users/lopezj/svn/modeling/sediment/
export C50=/home/workspace/ccalmr50/lopezj/
export SVN_EDITOR=vim
export PROC=$SVN/modeling/processing/trunk/processing/
export HOME2=/home/workspace/users/lopezj/
export DATA=/home/workspace/project/lopezj/
export PETSC_DIR=/home/workspace/users/lopezj/src/petsc
export PETSC_ARCH=linux-intel
export PETSC_O=linux-intel-O
export AG=/disk/ambfs21/0/users/lopezj/src/selfe_argonne/src
export SRC=$HOME2/src
export SELFE=/home/workspace/users/lopezj/src/selfe-refactor/src
export VALGRIND_LIB=/home/lopezj/lib/valgrind
export OC=/home/lopezj/sediment/nc_os14/scripts
export TIDES=/home/workspace/users/lopezj/tides
export SED=/home/workspace/ccalmr52/lopezj/sediment/db31_etm_runs

export LD_LIBRARY_PATH=$HOME/local/lib64:\
$HOME/local/lib:\
/opt/openmpi/intel/lib/:\
/opt/intel/vtune_amplifier_xe_2011/lib64/:\
/opt/openmpi/intel/lib/:\
$PETSC_DIR/$PETSC_O/lib:\
/usr/local/lib:\
$PETSC_DIR/$PETSC_O/lib

# Alias 
alias ll="ls -al"
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"
PS1="\u@\h:\w) "

alias paraview="/home/workspace/users/lopezj/src/ParaView-4.01.1-Linux-64bit/bin/paraview"
#alias ipython="/home/lopezj/local/bin/ipython"
alias cp_run="rsync -avl --exclude=outputs --exclude=images --exclude=data --exclude=*.mp4"

alias cmop="source ~/virt_env/cmop/bin/activate"
alias dev="source ~/virt_env/dev/bin/activate"
alias dev_27="source ~/virt_env/dev_27/bin/activate"

# Paths
PATH=.\
/usr/bin:\
/sbin:\
/usr/sbin:\
/usr/X11R6/bin:\
/usr/local/pgsql/bin:\
/usr/local/bin:\
/usr/local/ace/bin:\
/usr/local/netcdf/bin:\
/home/workspace/project/lopezj/scripts:\
/usr/local/cmop/bin:\
/usr/local/selfe/bin:\
/home/lopezj/.local/bin:\
$PATH; export PATH

# add in Intel compilers
if [ -f /opt/intel/compiler70/ia32/bin/iccvars.sh ]; then
	FC=ifc ; export FC
	F90=ifc ; export F90
fi

# Need vi key bindings
set -o vi

# virtualenvwrapper
#source /home/lopezj/.local/bin/virtualenvwrapper.sh
export WORKON_HOME=/home/lopezj/virt_env

# added by Anaconda 2.1.0 installer
export PATH="/home/lopezj/.local/anaconda/bin:$PATH"
#export PYTHONPATH="/home/lopezj/.local/anaconda/lib/python2.7/site-packages/processing:/home/lopezj/.local/anaconda/lib/python2.7/site-packages/"
