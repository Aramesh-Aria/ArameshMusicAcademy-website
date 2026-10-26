# Programmes are separate from Instruments, and come in two kinds

The live data stored تئوری و سلفژ, گروه نوازی and موسیقی کودک as `Instrument` rows, because Instrument was the only way to say what a Teacher or ClassSession offers. They aren't instruments. They are ways of studying, which the redesign presents as Programme cards and Programme pages, separate from the instrument grid. We are adding a `Programme` model (staff can edit it in the admin) and moving those three rows out of Instrument with a data migration. Instrument now means only real instruments, and voice.

Programmes are not all scheduled the same way:
- **With the teacher** (private lessons, theory and solfège, children's music): taught whenever a Teacher who offers it is present. These hang off `Teacher` (M2M) and have no time of their own. The schedule shows them on every one of that Teacher's ClassSessions.
- **At a fixed time** (ensemble playing, Thursdays): a ClassSession is reserved for the Programme, and nothing else is taught in that slot. The reserved ClassSession names the Programme.

Private lessons are the default for the whole Academy, since every lesson there is private. They are never tagged on a Teacher or ClassSession; they are only a Programme the Visitor can read about.

## Considered Options

- **Keep the subjects as Instruments (status quo):** No migration, but the instrument grid would show "گروه نوازی" next to "سنتور". Programme pages couldn't exist, and the schedule couldn't tell a reserved ensemble slot from a normal one.
- **Programme on ClassSession only:** One link, but it would force theory onto specific days. The Academy doesn't schedule theory; a Teacher who offers it teaches it whenever they are in.
- **Programme on Teacher only:** Simple, but it can't express that Thursday is reserved for the ensemble and nothing else.
- **Teacher → Programme for "with the teacher", plus a ClassSession → Programme reservation for "at a fixed time" (chosen):** It matches how the Academy actually works, at the cost of two relationships and a rule in the schedule view.
