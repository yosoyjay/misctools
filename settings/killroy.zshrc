# Path to your oh-my-zsh configuration.
ZSH=$HOME/.oh-my-zsh

# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="alanpeabody"

# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

# Set to this to use case-sensitive completion
CASE_SENSITIVE="true"

# Uncomment this to disable bi-weekly auto-update checks
# DISABLE_AUTO_UPDATE="true"

# Uncomment to change how often before auto-updates occur? (in days)
# export UPDATE_ZSH_DAYS=13

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want to disable command autocorrection
# DISABLE_CORRECTION="true"

# Uncomment following line if you want red dots to be displayed while waiting for completion
# COMPLETION_WAITING_DOTS="true"

# Uncomment following line if you want to disable marking untracked files under
# VCS as dirty. This makes repository status check for large repositories much,
# much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
plugins=(git osx python)

source $ZSH/oh-my-zsh.sh

# Customize to your needs...
export PATH=$HOME/anaconda/bin:\
/usr/local/bin:\
/usr/local/sbin:\
/usr/bin:\
/bin:\
/usr/sbin:\
/sbin:\
/opt/X11/bin:\
/usr/local/git/bin:\
/usr/texbin:\
/usr/local/texlive/2014/bin/x86_64-darwin

# Vi mode, set delay between modes to 0.1 seconds, not default 0.4
bindkey -v
export KEYTIMEOUT=1
bindkey "^R" history-incremental-search-backward

#-----------------------------------------------------------------------------
# From .bashrc
#-----------------------------------------------------------------------------

# Aliases
alias rm='rm -i'
#alias ll='ls -Al'
alias ls='ls -GFh'
alias ..='cd ..'
export SELFE=$HOME/src/selfe-refactor/src 

# Work related ssh 
alias sirius='ssh -Y lopezj@sirius.stccmop.org' 
alias ambcs03='ssh -Y lopezj@ambcs03.stccmop.org'
alias ambcs01='ssh -Y lopezj@ambcs01.stccmop.org'
alias vega='ssh -Y lopezj@vega.stccmop.org'
alias rigilk='ssh -AY lopezj@rigilk.stccmop.org'
alias arcturus='ssh -Y lopezj@arcturus1.stccmop.org'
alias 6400='ssh -Y lopezj@amb6400a.stccmop.org'
alias carver='ssh -Y lopezj@carver.nersc.gov'
alias hopper='ssh -Y lopezj@hopper.nersc.gov' 
alias edison='ssh -Y lopezj@edison.nersc.gov'
alias stamp='ssh -Y lopezj@stampede.tacc.utexas.edu'

# ETM Cruise APL boxen
alias ubu='ssh jesse@10.128.240.174'
alias hertz='ssh jesse@10.128.240.220'

# Paths
export PYTHONPATH=/Users/jesse/lib/:\
$DB:\
$HOME/src/:\
$DB/src/CODAS/:\
$HOME/anaconda/lib/python2.7/site-packages/processing

# NETCDF exports for GOTM
export NETCDFHOME=/usr/local/
export NETCDFINC=/usr/local/include
export NETCDFLIBNAME=libnetcdff.a

# PETSc
export PETSC_DIR=/Users/jesse/src/petsc
export PETSC_ARCH=osx-gnu-O
export PETSC_O=osx-gnu-O
export LD_LIBRARY_PATH=${PETSC_DIR}/${PETSC_ARCH}/lib
export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH

# Use omnicomplete
alias vi="vim_wrapper"


# Python
# Only run pip if a virtualenv is activated
#export PIP_REQUIRE_VIRTUALENV=true
# Cache pip-installed packages to avoid downloads
export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache

# virtualenvwarpper
export PROJECT_HOME=~/
export WORKON_HOME=~/virutal_envs
source /usr/local/bin/virtualenvwrapper.sh
#export PIP_REQUIRE_VIRTUALENV=true
export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache

# HOSTNAME because OS X doesn't set it and it's needed in processing
export HOSTNAME='killroy'

# Spark stuff
# for the CDH-installed Spark
export SPARK_HOME='/Users/jesse/Downloads/spark-1.4.1/'
  
# this is where you specify all the options you would normally add after bin/pyspark
export PYSPARK_SUBMIT_ARGS='--master local[2] pyspark-shell' 
#export PYSPARK_SUBMIT_ARGS='--master yarn --deploy-mode client --num-executors 24 --executor-memory 10g --executor-cores 5'
