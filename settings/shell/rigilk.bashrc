# -*- shell-script -*-
# TACC startup script: ~/.bashrc version 2.1 -- 12/17/2013


# This file is NOT automatically sourced for login shells.
# Your ~/.profile can and should "source" this file.

# Note neither ~/.profile nor ~/.bashrc are sourced automatically by
# bash scripts. However, a script inherits the environment variables
# from its parent shell.  Both of these facts are standard bash
# behavior.
#
# In a parallel mpi job, this file (~/.bashrc) is sourced on every 
# node so it is important that actions here not tax the file system.
# Each nodes' environment during an MPI job has ENVIRONMENT set to
# "BATCH" and the prompt variable PS1 empty.

#################################################################
# Optional Startup Script tracking. Normally DBG_ECHO does nothing
if [ -n "$SHELL_STARTUP_DEBUG" ]; then
  DBG_ECHO "${DBG_INDENT}~/.bashrc{"
fi

############
# SECTION 1
#
# There are three independent and safe ways to modify the standard
# module setup. Below are three ways from the simplest to hardest.
#   a) Use "module save"  (see "module help" for details).
#   b) Place module commands in ~/.modules
#   c) Place module commands in this file inside the if block below.
#
# Note that you should only do one of the above.  You do not want
# to override the inherited module environment by having module
# commands outside of the if block[3].

if [ -z "$__BASHRC_SOURCED__" -a "$ENVIRONMENT" != BATCH ]; then
  export __BASHRC_SOURCED__=1

  ##################################################################
  # **** PLACE MODULE COMMANDS HERE and ONLY HERE.              ****
  ##################################################################

#  module add mvapich2/1.9a2
#  module add python/2.7.3-epd-7.3.2
  module add python
  module add intel 
  module add hdf5/1.8.9
  module add netcdf/4.2.1.1 # NOTE remove for slim!
  module swap hdf5 phdf5/1.8.9 # needed for refactored selfe
  module add pmetis/3.2.0
  module add petsc/3.4
#  module add tau
#  module add valgrind
#  module add hpctoolkit
wait
fi

############
# SECTION 2
#
# Please set or modify any environment variables inside the if block
# below.  For example, modifying PATH or other path like variables
# (e.g LD_LIBRARY_PATH), the guard variable (__PERSONAL_PATH___) 
# prevents your PATH from having duplicate directories on sub-shells.

if [ -z "$__PERSONAL_PATH__" ]; then
  export __PERSONAL_PATH__=1

  ###################################################################
  # **** PLACE Environment Variables including PATH here.        ****
  ###################################################################

   # Path
   export PATH=$PATH:$HOME/local/bin:$HOME/src/misctools/hpc:$HOME/.local/bin
   #export PATH=~/bin:/home1/02454/karnat/local/bin:$PATH
   export LD_LIBRARY_PATH=$HOME/local/lib/:$LD_LIBRARY_PATH
  
   # Python
   export PYTHONPATH=$PYTHONPATH:$HOME/local/lib/python2.7/site-packages/processing:$HOME/local/lib/python2.7/site-packages
fi

########################
# SECTION 3
#
# Controling the prompt: Suppose you want stampede1(14)$  instead of 
# login1.stampede(14)$ 
# 
if [ -n "$PS1" ]; then
#   myhost=$(hostname -f)              # get the full hostname
#   myhost=${myhost%.tacc.utexas.edu}  # remove .tacc.utexas.edu
#   first=${myhost%%.*}                # get the 1st name (e.g. login1)
#   SYSHOST=${myhost#*.}               # get the 2nd name (e.g. stampede)
#   first5=$(expr substr $first 1 5)   # get first 5 character from $first
#   if [ "$first5" = "login" ]; then
#     num=$(expr $first : '[^0-9]*\([0-9]*\)') # get the number
#     HOST=${SYSHOST}$num                      # HOST -> stampede1
#   else
#     # first is not login1 so take first letter of system name
#     L=$(expr substr $SYSHOST 1 1 | tr '[:lower:]' '[:upper:]')
#
#     #  If host is c521-101.stampeded then
#     HOST=$L$first      # HOST  -> Sc521-101 
#   fi
#   PS1='$HOST(\#)\$ '   # Prompt either stampede1(14)$ or Sc521-101(14)$ 

    PROMPT_COMMAND='printf "\033]0;%s@%s:%s\033\\" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/~}"'
    PS1="\u@\h:\w) "
fi
#####################################################################
# **** Place any else below.                                     ****
#####################################################################

# alias m="more"
alias bls='/bin/ls'   # handy alias for listing a large directory.
alias rm='/bin/rm -i'

# vi keybindings
set -o vi

# append history and increase length
shopt -s histappend
HISTFILESIZE=2500

# inputrc
export INPUTRC=$HOME/.inputrc

##########
# Umask
#
# If you are in a group that wishes to share files you can use 
# "umask". to make your files be group readable.  Placing umask here 
# is the only reliable place for bash and will insure that it is set 
# in all types of bash shells.

umask 022

###################################
# Optional Startup Script tracking 

if [ -n "$SHELL_STARTUP_DEBUG" ]; then
  DBG_ECHO "${DBG_INDENT}}"
fi

