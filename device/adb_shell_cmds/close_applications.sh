APPS=$(dumpsys window a | grep "/" | cut -d "{" -f2 | cut -d "/" -f1 | cut -d " " -f2)

for APP in $APPS ; do
  if [[ ! ("$APP" == *"nexuslauncher"*) ]]; then
    echo "Closing: $APP"
    pm clear $APP
  fi
done
