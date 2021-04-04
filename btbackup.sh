TODAY=$(date +%Y.%m.%d)
WHAT="/backup/all"
DEST="/backup/.snapshots/backup-$TODAY"

echo "=== Running backup - $(date) ==="
if [[ -d $DEST ]]; then
  echo "Backup $DEST already exists. Ignoring."
  exit
fi

CMD="sudo btrfs subvolume snapshot $WHAT $DEST"
$CMD