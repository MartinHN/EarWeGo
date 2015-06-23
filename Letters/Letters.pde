/**
 * Letters. 
 * 
 * Draws letters to the screen. This requires loading a font, 
 * setting the font, and then drawing the letters.
 */

PFont f, fBig;

String[] chords = {"A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"};

/**
 * oscP5sendreceive by andreas schlegel
 * example shows how to send and receive osc messages.
 * oscP5 website at http://www.sojamo.de/oscP5
 */
 
import oscP5.*;
import netP5.*;

String currentChord = "";
String chordType = "";

int chordHeight, chordWidth;
  
OscP5 oscP5;
NetAddress myRemoteLocation;

/* incoming osc message are forwarded to the oscEvent method. */
void oscEvent(OscMessage theOscMessage) {
  /* print the address pattern and the typetag of the received OscMessage */
  print("### received an osc message.");
  print(" addrpattern: "+theOscMessage.addrPattern());
  println(" typetag: "+theOscMessage.typetag());
  
  currentChord = theOscMessage.get(1).stringValue();
  chordType = theOscMessage.get(0).stringValue();
}

void setup() {
  size(1024, 900);
  background(0);
  
  chordWidth = 1024;
  chordHeight = 400;
  
    

  // Create the font
  printArray(PFont.list());
  f = createFont("Georgia", 28);
  fBig = createFont("Georgia", 38);
  
//  f = createFont("Georgia", 28);
//  fBig = createFont("Georgia", 38);  
  textFont(f);
  textAlign(CENTER, CENTER);
  
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this,4446);  
}

int indexOfString(String stringToFind)
{
  int returnValue = 0;
  for(int i=0; i<chords.length; i++) {
    println(stringToFind);
    println(chords[i]);    
    if(stringToFind.equals(chords[i])) {         
      returnValue = i;
    }
  }
  return returnValue;
}

void draw() {
  background(0);

  // Set the left and top margin
  int margin = 10;
  translate(margin*4, margin*4);

  int gap = 46;
  int counter = 0;
  
  int index = indexOfString(currentChord);  
  
  for (int y = 0; y < chordHeight-gap; y += gap) {
    for (int x = 0; x < chordWidth-gap; x += gap) {
                     
      if (counter == index) {
        fill(255, 204, 0);
        textFont(fBig);
      } 
      else {
        fill(255);
        textFont(f);
      }

      // Draw the letter to the screen
      text(chords[counter], x, y);

      // Increment the counter
      counter++;
      if(counter >= 12)
        counter = 0;
    }
  }
  
  if(chordType.equals("major")) {
    fill(255, 204, 0);
    textFont(fBig);
  }
  else {
    fill(255);
    textFont(f);
  }
  
  text("Major", 275, 400);  
  
  if(chordType.equals("minor")) {
    fill(255, 204, 0);
    textFont(fBig);
  }
  else {
    fill(255);
    textFont(f);
  }
  text("Minor", 375, 400);  
  
}

